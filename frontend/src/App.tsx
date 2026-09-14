import React, { useState } from 'react'
import { UploadCloud, FileType, CheckCircle, RefreshCcw, ShieldCheck, Zap, Sparkles, Trash2, Download } from 'lucide-react'
import axios from 'axios'

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [targetFormat, setTargetFormat] = useState('')
  const [status, setStatus] = useState<'idle' | 'converting' | 'success' | 'error'>('idle')
  const [downloadUrl, setDownloadUrl] = useState('')
  const [isDragging, setIsDragging] = useState(false)

  // File ki extension nikalne ka function
  const getFileExtension = (filename: string) => {
    return filename.slice((filename.lastIndexOf('.') - 1 >>> 0) + 2).toLowerCase()
  }

  // File ke lihaz se smart target formats dene ka function
  const getAvailableFormats = () => {
    if (!file) return []
    const ext = getFileExtension(file.name)

    // Images
    if (['png', 'jpg', 'jpeg', 'webp'].includes(ext)) {
      return [
        { value: 'png', label: 'PNG Image (.png)' },
        { value: 'jpg', label: 'JPG Image (.jpg)' },
        { value: 'webp', label: 'WEBP Image (.webp)' },
        { value: 'pdf', label: 'PDF Document (.pdf)' }
      ]
    }
    // Documents
    if (ext === 'docx' || ext === 'doc') {
      return [
        { value: 'pdf', label: 'PDF Document (.pdf)' },
        { value: 'txt', label: 'Plain Text (.txt)' }
      ]
    }
    if (ext === 'pdf') {
      return [
        { value: 'docx', label: 'Word Document (.docx)' },
        { value: 'png', label: 'PNG Image (.png)' }
      ]
    }
    // Spreadsheets (Excel)
    if (['xlsx', 'xls', 'csv'].includes(ext)) {
      return [
        { value: 'pdf', label: 'PDF Document (.pdf)' },
        { value: 'csv', label: 'CSV Format (.csv)' },
        { value: 'xlsx', label: 'Excel Sheet (.xlsx)' }
      ]
    }
    // Presentations (PowerPoint)
    if (['pptx', 'ppt'].includes(ext)) {
      return [
        { value: 'pdf', label: 'PDF Document (.pdf)' },
        { value: 'png', label: 'Slides as Images (.png)' }
      ]
    }

    // Default fallback
    return [{ value: 'pdf', label: 'PDF Document (.pdf)' }]
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const selectedFile = e.target.files[0]
      setFile(selectedFile)
      setStatus('idle')
      
      // Jaise hi file aaye, pehla available format default set kar dein
      const formats = getAvailableFormats()
      if (formats.length > 0) {
        setTargetFormat(formats[0].value)
      }
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const droppedFile = e.dataTransfer.files[0]
      setFile(droppedFile)
      setStatus('idle')
      
      const formats = getAvailableFormats()
      if (formats.length > 0) {
        setTargetFormat(formats[0].value)
      }
    }
  }

  const handleConvert = async () => {
    if (!file) return

    setStatus('converting')
    const formData = new FormData()
    formData.append('file', file)
    formData.append('target_format', targetFormat)

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/convert', formData)
      if (response.data.success) {
        setStatus('success')
        setDownloadUrl(response.data.download_url)
      }
    } catch (error) {
      console.error(error)
      setStatus('error')
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const availableFormats = getAvailableFormats()

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-emerald-950 text-slate-100 flex flex-col font-sans selection:bg-emerald-500 selection:text-white">
      
      {/* Navigation Bar */}
      <header className="border-b border-slate-700/50 backdrop-blur-md bg-slate-900/60 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-tr from-emerald-500 to-teal-400 text-slate-950 p-2.5 rounded-xl shadow-lg shadow-emerald-500/20 font-black">
              <FileType size={24} />
            </div>
            <span className="text-2xl font-black tracking-tight text-white">Convert<span className="text-emerald-400">X</span></span>
          </div>
          <div className="hidden md:flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/20 px-4 py-1.5 rounded-full text-emerald-400 text-sm font-medium">
            <Sparkles size={16} /> Universal File Engine
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-grow flex flex-col items-center justify-center px-4 py-12">
        
        {/* Hero Section */}
        <div className="text-center max-w-2xl mb-10">
          <h1 className="text-4xl md:text-6xl font-black tracking-tight mb-4 bg-gradient-to-r from-white via-slate-200 to-emerald-400 bg-clip-text text-transparent">
            Smart Universal Converter
          </h1>
          <p className="text-slate-400 text-lg md:text-xl font-normal">
            Convert images, documents, spreadsheets, and presentations instantly with smart validation.
          </p>
        </div>

        {/* Card Box */}
        <div className="max-w-xl w-full bg-slate-900/80 backdrop-blur-xl border border-slate-700/60 rounded-3xl shadow-2xl shadow-emerald-950/30 p-8 relative overflow-hidden">
          
          <div className="absolute -top-24 -right-24 w-48 h-48 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>

          {!file ? (
            <label 
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              className={`flex flex-col items-center justify-center w-full h-72 border-2 border-dashed rounded-2xl cursor-pointer transition-all duration-300 ${
                isDragging 
                  ? 'border-emerald-400 bg-emerald-500/10 scale-[1.01]' 
                  : 'border-slate-700 bg-slate-800/50 hover:bg-slate-800 hover:border-emerald-500/50'
              }`}
            >
              <div className="bg-emerald-500/10 p-4 rounded-2xl text-emerald-400 mb-4 ring-8 ring-emerald-500/5">
                <UploadCloud className="w-10 h-10" />
              </div>
              <p className="text-lg font-bold text-slate-200 mb-1">Click to upload or drag & drop</p>
              <p className="text-xs text-slate-400 tracking-wide uppercase font-semibold">Supports Images, PDF, Word, Excel, PPT</p>
              <input type="file" className="hidden" onChange={handleFileChange} />
            </label>
          ) : (
            <div className="space-y-6">
              
              {/* File Info Box */}
              <div className="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-4 flex items-center justify-between">
                <div className="flex items-center gap-4 overflow-hidden">
                  <div className="bg-emerald-500/10 text-emerald-400 p-3 rounded-xl">
                    <FileType size={24} />
                  </div>
                  <div className="overflow-hidden">
                    <h4 className="font-bold text-slate-200 truncate">{file.name}</h4>
                    <p className="text-xs text-slate-400">{formatFileSize(file.size)}</p>
                  </div>
                </div>
                <button 
                  onClick={() => { setFile(null); setStatus('idle'); }} 
                  className="text-slate-400 hover:text-red-400 p-2 rounded-lg hover:bg-red-500/10 transition"
                  title="Remove file"
                >
                  <Trash2 size={18} />
                </button>
              </div>

              {/* Smart Format Select Dropdown */}
              <div className="space-y-2">
                <label className="text-xs font-bold uppercase tracking-wider text-slate-400">Available Target Formats</label>
                <select 
                  value={targetFormat} 
                  onChange={(e) => {
                    setTargetFormat(e.target.value)
                    setStatus('idle')
                  }}
                  className="w-full bg-slate-800 border border-slate-700 text-slate-100 font-semibold text-sm rounded-xl px-4 py-3.5 focus:outline-none focus:border-emerald-500 transition"
                >
                  {availableFormats.map((fmt) => (
                    <option key={fmt.value} value={fmt.value}>
                      {fmt.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Actions */}
              {status === 'idle' && (
                <button 
                  onClick={handleConvert}
                  className="w-full bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-black py-4 rounded-xl transition-all shadow-lg shadow-emerald-500/25 flex items-center justify-center gap-2 transform active:scale-[0.99]"
                >
                  <Zap size={20} className="fill-slate-950" /> Convert Now
                </button>
              )}

              {status === 'converting' && (
                <button disabled className="w-full bg-slate-800 text-emerald-400 font-bold py-4 rounded-xl flex items-center justify-center gap-3 cursor-not-allowed border border-emerald-500/20">
                  <RefreshCcw size={20} className="animate-spin text-emerald-400" /> Processing conversion...
                </button>
              )}

              {status === 'success' && (
                <div className="space-y-4 pt-2">
                  <div className="flex items-center justify-center gap-2 text-emerald-400 font-bold bg-emerald-500/10 border border-emerald-500/20 py-3 rounded-xl">
                    <CheckCircle size={20} /> Conversion Successful!
                  </div>
                  <a 
                    href={downloadUrl}
                    download
                    className="w-full inline-flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-500 text-white font-bold py-4 rounded-xl transition-all shadow-lg shadow-blue-600/30"
                  >
                    <Download size={20} /> Download Converted File
                  </a>
                </div>
              )}

              {status === 'error' && (
                <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-center font-medium py-3 rounded-xl text-sm">
                  Conversion failed. Please ensure backend conversion handler supports this format.
                </div>
              )}

            </div>
          )}

        </div>

        {/* Feature Badges Footer */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-2xl w-full mt-16 text-center">
          <div className="flex items-center justify-center gap-3 bg-slate-900/40 border border-slate-800 p-4 rounded-2xl">
            <Zap className="text-emerald-400 w-5 h-5 flex-shrink-0" />
            <span className="text-sm font-medium text-slate-300">Smart Format Detection</span>
          </div>
          <div className="flex items-center justify-center gap-3 bg-slate-900/40 border border-slate-800 p-4 rounded-2xl">
            <ShieldCheck className="text-emerald-400 w-5 h-5 flex-shrink-0" />
            <span className="text-sm font-medium text-slate-300">100% Private & Secure</span>
          </div>
          <div className="flex items-center justify-center gap-3 bg-slate-900/40 border border-slate-800 p-4 rounded-2xl">
            <Sparkles className="text-emerald-400 w-5 h-5 flex-shrink-0" />
            <span className="text-sm font-medium text-slate-300">Universal Engine</span>
          </div>
        </div>

      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
        © 2026 ConvertX Engine. Built with FastAPI & React.
      </footer>

    </div>
  )
}

export default App