import { useAuth } from '../../context/AuthContext';
import { Navigate, useLocation } from 'react-router-dom';


function ProtectedRoute({ children, roles}){
    const { token, role } = useAuth();
    const location = useLocation();
    
    if (!token) {
       return <Navigate state={{ from: location }} to="/login" replace />
    }
    if (roles && !roles.includes(role)) {
        return <Navigate to="/" replace />
    }
    return children
}

export default ProtectedRoute