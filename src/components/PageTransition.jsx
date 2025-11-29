export default function PageTransition({ children }) {
  return (
    <div className="animate-fadeIn">
      {children}
    </div>
  );
}
