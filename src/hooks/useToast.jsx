import { useState } from "react";
import Toast from "../components/Toast";

export default function useToast() {
  const [toast, setToast] = useState(null);

  function showToast(message, type = "success") {
    setToast({ message, type });
  }

  function ToastContainer() {
    if (!toast) return null;
    return <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />;
  }

  return { showToast, ToastContainer };
}
