import React from 'react';
import { motion } from 'framer-motion';
import { Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/Button';

const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.5 },
};

const ResumeAnalysis = () => {
  const [file, setFile] = React.useState<File | null>(null);
  const [isAnalyzing, setIsAnalyzing] = React.useState(false);
  const [score, setScore] = React.useState<number | null>(null);

  // Placeholder data for demo
  const analysisResults = {
    score: 85,
    missingKeywords: ['leadership', 'project management', 'agile'],
    suggestions: [
      'Add more quantifiable achievements',
      'Include leadership experience',
      'Highlight project management skills',
    ],
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile?.type === 'application/pdf') {
      setFile(droppedFile);
    }
  };

  const handleAnalyze = async () => {
    setIsAnalyzing(true);
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 2000));
    setScore(analysisResults.score);
    setIsAnalyzing(false);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <motion.div {...fadeInUp} className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900">Resume Analysis</h1>
        <p className="mt-4 text-lg text-gray-600">
          Upload your resume to get an ATS compatibility score and improvement suggestions
        </p>
      </motion.div>

      {!file ? (
        <motion.div
          {...fadeInUp}
          className="mt-8"
          onDragOver={(e) => e.preventDefault()}
          onDrop={handleDrop}
        >
          <div className="flex flex-col items-center justify-center w-full h-64 border-2 border-dashed border-gray-300 rounded-2xl bg-gray-50 hover:bg-gray-100 transition-colors cursor-pointer">
            <Upload className="h-10 w-10 text-gray-400 mb-4" />
            <p className="text-gray-600">
              Drag and drop your resume PDF here, or{' '}
              <span className="text-gray-900 font-medium">browse files</span>
            </p>
            <p className="text-sm text-gray-500 mt-2">Maximum file size: 10MB</p>
          </div>
        </motion.div>
      ) : (
        <motion.div {...fadeInUp} className="mt-8 space-y-8">
          <div className="bg-white rounded-2xl p-6 shadow-sm">
            <div className="flex items-center space-x-4">
              <div className="p-3 bg-gray-100 rounded-xl">
                <FileText className="h-6 w-6 text-gray-700" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">{file.name}</h3>
                <p className="text-sm text-gray-500">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>

            <div className="mt-6">
              <Button
                onClick={handleAnalyze}
                isLoading={isAnalyzing}
                variant="glow"
                size="lg"
                className="w-full"
              >
                Analyze Resume
              </Button>
            </div>
          </div>

          {score !== null && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-2xl p-6 shadow-sm"
            >
              <h3 className="text-xl font-semibold text-gray-900 mb-6">Analysis Results</h3>

              {/* Score */}
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl mb-6">
                <div>
                  <p className="text-sm font-medium text-gray-600">ATS Compatibility Score</p>
                  <p className="text-3xl font-bold text-gray-900">{score}%</p>
                </div>
                {score >= 80 ? (
                  <CheckCircle className="h-8 w-8 text-green-500" />
                ) : (
                  <AlertCircle className="h-8 w-8 text-amber-500" />
                )}
              </div>

              {/* Missing Keywords */}
              <div className="mb-6">
                <h4 className="text-sm font-medium text-gray-900 mb-3">Missing Keywords</h4>
                <div className="flex flex-wrap gap-2">
                  {analysisResults.missingKeywords.map((keyword) => (
                    <span
                      key={keyword}
                      className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-red-50 text-red-700"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>

              {/* Suggestions */}
              <div>
                <h4 className="text-sm font-medium text-gray-900 mb-3">Suggestions</h4>
                <ul className="space-y-3">
                  {analysisResults.suggestions.map((suggestion, index) => (
                    <li
                      key={index}
                      className="flex items-start space-x-3 text-gray-600"
                    >
                      <span className="flex-shrink-0 w-5 h-5 rounded-full bg-gray-100 flex items-center justify-center text-xs font-medium text-gray-900">
                        {index + 1}
                      </span>
                      <span>{suggestion}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Download Report Button */}
              <div className="mt-8">
                <Button variant="outline" size="lg" className="w-full">
                  Download Detailed Report
                </Button>
              </div>
            </motion.div>
          )}
        </motion.div>
      )}
    </div>
  );
};

export default ResumeAnalysis; 