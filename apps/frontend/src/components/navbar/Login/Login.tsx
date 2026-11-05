// src/components/navbar/Login/Login.tsx
import { Link } from 'react-router-dom'

export default function Login() {
    return <Link to="/login">Login</Link>   // note: `to`, not `href`
}

const GoToLogin: React.FC = () =>  {

    return (
        <>
            <a href="pages/compte/login.tsx" className="navbar_choices">Login</a>
        </>
    )
}

export default GoToLogin
