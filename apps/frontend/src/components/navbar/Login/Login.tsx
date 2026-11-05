import type React from 'react'

type Props = { onLoginClick: () => void }

const GoToLogin: React.FC<Props> = ({ onLoginClick }) => {
    return (
        <button type="button" className="navbar_choices" onClick={onLoginClick}>
            Login
        </button>
    )
}

export default GoToLogin