import { useState } from "react";

const DownloadReportButtons = ({ results, productName, weightGrams, fragility }) => {
  const [downloadingPDF, setDownloadingPDF] = useState(false);
  const [downloadingExcel, setDownloadingExcel] = useState(false);
  const [pdfError, setPDFError] = useState(null);
  const [excelError, setExcelError] = useState(null);

  const buildReportPayload = () => {
    return {
      product_name: productName,
      product_weight_grams: weightGrams,
      fragility: fragility,
      generated_at: new Date().toISOString(),
      recommendations: results?.recommendations || [],
    };
  };

  const handleDownloadPDF = async () => {
    try {
      setDownloadingPDF(true);
      setPDFError(null);

      const payload = buildReportPayload();

      const response = await fetch("/api/report/pdf", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to generate PDF");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `EcoPackAI_${productName}_Report.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      setDownloadingPDF(false);
    } catch (error) {
      console.error("PDF download error:", error);
      setPDFError(error.message || "Error downloading PDF. Please try again.");
      setDownloadingPDF(false);
    }
  };

  const handleDownloadExcel = async () => {
    try {
      setDownloadingExcel(true);
      setExcelError(null);

      const payload = buildReportPayload();

      const response = await fetch("/api/report/excel", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to generate Excel");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `EcoPackAI_${productName}_Report.xlsx`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      setDownloadingExcel(false);
    } catch (error) {
      console.error("Excel download error:", error);
      setExcelError(error.message || "Error downloading Excel. Please try again.");
      setDownloadingExcel(false);
    }
  };

  const isAnyDownloading = downloadingPDF || downloadingExcel;

  return (
    <section className="mx-auto w-full max-w-7xl">
      <div className="rounded-2xl border border-green-100 bg-white p-6 shadow-lg">
        {/* Header */}
        <div className="mb-4 flex items-center gap-2">
          <svg
            className="h-6 w-6 text-green-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
            />
          </svg>
          <div>
            <h3 className="text-lg font-bold text-slate-800">Download Report</h3>
            <p className="text-sm text-slate-600">
              Get your top 5 recommendations as a formatted report
            </p>
          </div>
        </div>

        {/* Buttons Container */}
        <div className="flex flex-col gap-4 sm:flex-row sm:gap-4">
          {/* PDF Button */}
          <div className="flex-1">
            <button
              onClick={handleDownloadPDF}
              disabled={isAnyDownloading}
              className="flex w-full items-center justify-center gap-2 rounded-xl border-2 border-red-500 px-6 py-3 font-semibold text-red-500 transition-all duration-300 hover:bg-red-500 hover:text-white disabled:cursor-not-allowed disabled:opacity-50"
            >
              {downloadingPDF ? (
                <>
                  <svg
                    className="h-5 w-5 animate-spin"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                    />
                  </svg>
                  <span>Generating PDF...</span>
                </>
              ) : (
                <>
                  <svg
                    className="h-5 w-5"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M7 19H5v-2h2v2zm4 0H9v-2h2v2zm4 0h-2v-2h2v2zm2-6h-2v-2h2v2zm-4 0h-2v-2h2v2zm-4 0H7v-2h2v2zm8-2v2h2v-2h-2zm0-8H3c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14v-2H3v-2h14V8zm4 4h-2v2h2V4zm0 6h-2v2h2v-2z" />
                  </svg>
                  <span>Download PDF Report</span>
                </>
              )}
            </button>
            {pdfError && (
              <p className="mt-2 text-xs text-red-500">
                {pdfError}
              </p>
            )}
          </div>

          {/* Excel Button */}
          <div className="flex-1">
            <button
              onClick={handleDownloadExcel}
              disabled={isAnyDownloading}
              className="flex w-full items-center justify-center gap-2 rounded-xl border-2 border-green-500 px-6 py-3 font-semibold text-green-600 transition-all duration-300 hover:bg-green-500 hover:text-white disabled:cursor-not-allowed disabled:opacity-50"
            >
              {downloadingExcel ? (
                <>
                  <svg
                    className="h-5 w-5 animate-spin"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                    />
                  </svg>
                  <span>Generating Excel...</span>
                </>
              ) : (
                <>
                  <svg
                    className="h-5 w-5"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
                  </svg>
                  <span>Download Excel Report</span>
                </>
              )}
            </button>
            {excelError && (
              <p className="mt-2 text-xs text-red-500">
                {excelError}
              </p>
            )}
          </div>
        </div>

        {/* Info Text */}
        <p className="mt-3 text-xs text-gray-400">
          <strong>PDF:</strong> Includes formatted report with all material details. <strong>Excel:</strong> Includes 3 sheets: Summary, All Recommendations, and Detailed Profiles.
        </p>
      </div>
    </section>
  );
};

export default DownloadReportButtons;
