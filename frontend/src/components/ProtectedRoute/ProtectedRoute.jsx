import { useAuth } from '../../context/AuthContext';
import { Navigate } from 'react-router-dom';

function ProtectedRoute({ children, roles}){
    const { token, role } = useAuth();
    
    if (!token) {
       return <Navigate to="/login" replace />
    }
    if (roles && !roles.includes(role)) {
        return <Navigate to="/" replace />
    }
    return children
}

export default ProtectedRoute