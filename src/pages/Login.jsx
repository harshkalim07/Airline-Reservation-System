import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import Input from "../components/Input";
import useToast from "../hooks/useToast";
import { AuthContext } from "../context/AuthContext";

export default function Login() {
  const [form, setForm] = useState({ email: "", password: "" });
  const { login, loading } = useContext(AuthContext);
  const { showToast, ToastContainer } = useToast();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    
    console.log('Form submitted with:', form);
    
    const result = await login(form.email, form.password);
    
    console.log('Login result:', result);
    console.log('Result.error:', result.error);
    console.log('Result.success:', result.success);
    
    if (result.success) {
      showToast("Login successful!", "success");
      setForm({ email: "", password: "" });
      
      setTimeout(() => {
        navigate('/');
      }, 1000);
    } else {
      console.log('About to show toast with error:', result.error);
      showToast(result.error || "Invalid email or password", "error");
    }
  }

  return (
    <div className="max-w-md mx-auto card">
      <h2 className="text-2xl font-semibold mb-4 text-center">User Login</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input 
          label="Email" 
          type="email"
          value={form.email} 
          onChange={v => setForm({ ...form, email: v })}
        />
        <Input 
          label="Password" 
          type="password" 
          value={form.password} 
          onChange={v => setForm({ ...form, password: v })}
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