import GoToLogin from "./Login/Login.tsx";

type Props = { onLoginClick: () => void }

const Navbar: React.FC<Props> = ({ onLoginClick }) => {
    return (
        <nav>
            {/* tes autres liens */}
            <GoToLogin onLoginClick={onLoginClick} />
        </nav>
    )
}

export default Navbar