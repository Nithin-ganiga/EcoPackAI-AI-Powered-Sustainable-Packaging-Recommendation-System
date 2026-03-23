// This file renders a loading overlay to clearly indicate that recommendation analysis is in progress.

const LoadingSpinner = () => {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40">
      <div className="rounded-2xl bg-white p-8 text-center shadow-md ring-1 ring-slate-200">
        <div className="mx-auto h-12 w-12 animate-spin rounded-full border-4 border-eco-green border-t-transparent" />
        <p className="mt-4 text-sm font-semibold text-slate-700">
          Analyzing packaging options for your product...
        </p>
      </div>
    </div>
  );
};

export default LoadingSpinner;
