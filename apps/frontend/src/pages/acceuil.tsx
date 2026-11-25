import Navbar from '../components/navbar/Navbar.tsx'

function PageAcceuil({ onLoginClick }: { onLoginClick: () => void }) {
    return (
        <>
            <Navbar onLoginClick={onLoginClick} />
            <h1>PrestINT</h1>
            <h2>Prestations des clubs de l'INT</h2>
        </>
    )
}

export default PageAcceuil