// This file renders user-friendly error feedback so API or validation failures are visible and understandable.

const ErrorMessage = ({ message }) => {
  return (
    <div className="mx-auto w-full max-w-2xl rounded-2xl border border-red-300 bg-red-50 p-5 shadow-sm">
      <div>
        <h3 className="font-bold text-red-700">Unable to complete your request</h3>
        <p className="mt-1 text-sm text-red-600">{message}</p>
        <p className="mt-2 text-xs text-red-500">Please retry with a more specific product name or check API connectivity.</p>
      </div>
    </div>
  );
};

export default ErrorMessage;
