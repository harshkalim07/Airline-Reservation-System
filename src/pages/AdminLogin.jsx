import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import Input from "../components/Input";
import useToast from "../hooks/useToast";
import { AuthContext } from "../context/AuthContext";
import api from "../services/api";

export default function AdminLogin() {
  const [form, setForm] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false);

  const { setUser } = useContext(AuthContext);
  const navigate = useNavigate();
  const { showToast, ToastContainer } = useToast();

  async function handleSubmit(e) {
    e.preventDefault();

    if (!form.email || !form.password) {
      showToast("Please fill all fields", "error");
      return;
    }

    try {
      setLoading(true);

      const response = await api.post('/auth/admin/login', {
        email: form.email,
        password: form.password
      });

      const userData = {
        ...response.data.user,
        token: response.data.access_token
      };

      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('sim_user', JSON.stringify(userData));
      
      // Update AuthContext
      if (setUser) {
        setUser(userData);
      }

      showToast("Admin login successful!", "success");

      setTimeout(() => {
        window.location.href = '/admin/flights';
      }, 1000);

    } catch (error) {
      console.error('Admin login error:', error);
      showToast(
        error.response?.data?.error || "Invalid admin credentials",
        "error"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-md mx-auto card">
      <h2 className="text-2xl font-semibold mb-4 text-center">Admin Login</h2>

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
        <button 
          className="btn-primary w-full mt-3" 
          disabled={loading}
        >
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>

      <ToastContainer />
    </div>
  );
}