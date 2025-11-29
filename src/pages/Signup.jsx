import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import Input from "../components/Input";
import useToast from "../hooks/useToast";
import { AuthContext } from "../context/AuthContext";

export default function Signup() {
  const [form, setForm] = useState({ email: "", password: "", confirmPassword: "" });
  const { register, loading } = useContext(AuthContext);
  const { showToast, ToastContainer } = useToast();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    
    if (form.password !== form.confirmPassword) {
      showToast("Passwords don't match", "error");
      return;
    }

    if (form.password.length < 6) {
      showToast("Password must be at least 6 characters", "error");
      return;
    }

    const result = await register(form.email, form.password);
    
    if (result.success) {
      showToast("Signup successful!", "success");
      setForm({ email: "", password: "", confirmPassword: "" });
      
      setTimeout(() => {
        navigate('/');
      }, 1000);
    } else {
      showToast(result.error || "Signup failed", "error");
    }
  }

  return (
    <div className="max-w-md mx-auto card">
      <h2 className="text-2xl font-semibold mb-4 text-center">User Signup</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input 
          label="Email" 
          type="email"
          value={form.email} 
          onChange={v => setForm({ ...form, email: v })} 
          required
        />
        <Input 
          label="Password" 
          type="password" 
          value={form.password} 
          onChange={v => setForm({ ...form, password: v })} 
          required
        />
        <Input 
          label="Confirm Password" 
          type="password" 
          value={form.confirmPassword} 
          onChange={v => setForm({ ...form, confirmPassword: v })} 
          required
        />
        <button 
          className="btn-primary w-full mt-3"
          disabled={loading}
        >
          {loading ? 'Signing up...' : 'Sign Up'}
        </button>
      </form>
      <ToastContainer />
    </div>
  );
}