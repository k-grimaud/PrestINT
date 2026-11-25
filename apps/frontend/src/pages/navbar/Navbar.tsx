export type Page = 'services' | 'account'

type NavbarProps = {
  page: Page
  isLogged: boolean
  onNavigate: (page: Page) => void
}

function Navbar({ page, isLogged, onNavigate }: NavbarProps) {
  return (
    <nav className="navbar">
      <b>PrestINT</b>
      <button
        className={page === 'services' ? 'tab active' : 'tab'}
        onClick={() => onNavigate('services')}
      >
        Prestations
      </button>
      <button
        className={page === 'account' ? 'tab active' : 'tab'}
        onClick={() => onNavigate('account')}
      >
        {isLogged ? 'Compte' : 'Connexion'}
      </button>
    </nav>
  )
}

export default Navbar