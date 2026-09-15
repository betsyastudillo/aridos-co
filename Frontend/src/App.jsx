import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import { AuthProvider } from "./context/AuthContext"
import ProtectedRoute from "./components/ProtectedRoute"
import Login from "./pages/Login"


function OrdersPlaceholder() {
  return <h2 className="p-4">Aquí va el listado de pedidos (siguiente paso)</h2>
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/orders"
            element={
              <ProtectedRoute>
                <OrdersPlaceholder />
              </ProtectedRoute>
            }
            />
          <Route path="*" element={<Navigate to="/orders" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
