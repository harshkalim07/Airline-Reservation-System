import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Input from "../components/Input";
import useToast from "../hooks/useToast";
import api from "../services/api";

export default function AdminSignup() {
  const [form, setForm] = useState({
    email: "",
    password: "",
    secret: ""
  });
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();
  const { showToast, ToastContainer } = useToast();

  async function handleSubmit(e) {
    e.preventDefault();

    if (!form.email || !form.password || !form.secret) {
      showToast("Please fill all fields", "error");
      return;
    }

    if (form.secret !== "ADMIN123") {
      showToast("Invalid admin secret key", "error");
      return;
    }

    try {
      setLoading(true);

      const response = await api.post('/auth/admin/signup', {
        email: form.email,
        password: form.password
      });

      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('sim_user', JSON.stringify(response.data.user));

      showToast("Admin account created!", "success");

      setTimeout(() => {
        navigate('/admin/login');
      }, 1000);

    } catch (error) {
      console.error('Admin signup error:', error);
      showToast(
        error.response?.data?.error || "Signup failed",
        "error"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-md mx-auto card">
      <h2 className="text-2xl font-semibold mb-4 text-center">Admin Signup</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <Input 
          label="Email" 
          value={form.email} 
          onChange={v => setForm({ ...form, email: v })} 
          disabled={loading}
        />
        <Input 
          label="Password" 
          type="password" 
          value={form.password} 
          onChange={v => setForm({ ...form, password: v })} 
          disabled={loading}
        />
        <Input 
          label="Secret Key" 
          value={form.secret} 
          onChange={v => setForm({ ...form, secret: v })} 
          disabled={loading}
        />

        <button 
          className="btn-primary w-full mt-2" 
          disabled={loading}
        >
          {loading ? 'Creating...' : 'Create Admin Account'}
        </button>
      </form>

      <ToastContainer />
    </div>
  );
}