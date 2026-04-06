const ExportButtons = ({ onExportPDF, onExportExcel, exportingPDF, exportingExcel }) => {
  return (
    <div className="flex flex-wrap items-center justify-end gap-3">
      <button
        type="button"
        onClick={onExportPDF}
        disabled={exportingPDF}
        className="inline-flex items-center gap-2 rounded-xl border border-rose-500 px-4 py-2.5 text-sm font-semibold text-rose-600 transition hover:bg-rose-500 hover:text-white disabled:cursor-not-allowed disabled:opacity-60"
      >
        <span aria-hidden="true">📄</span>
        {exportingPDF ? "Generating PDF..." : "Export PDF Report"}
      </button>

      <button
        type="button"
        onClick={onExportExcel}
        disabled={exportingExcel}
        className="inline-flex items-center gap-2 rounded-xl border border-emerald-600 px-4 py-2.5 text-sm font-semibold text-emerald-700 transition hover:bg-emerald-600 hover:text-white disabled:cursor-not-allowed disabled:opacity-60"
      >
        <span aria-hidden="true">📊</span>
        {exportingExcel ? "Generating Excel..." : "Export Excel Report"}
      </button>
    </div>
  );
};

export default ExportButtons;
