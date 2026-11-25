// Defining custom messages for some HTTP error codes
const MESSAGES: Record<number, string> = {
    404: "Cette page n'existe pas.",
    500: "Une erreur est survenue, réessayez plus tard.",
    502:"Le serveur ne répond pas, réessayez dans quelques instants.",
    503:"Serveur injoignable, réessayez à nouveau dans quelques instants.",
    504:"Délais de réponse du serveur dépassé, réessayez ultérieurement.",
}

function Erreur({ status }: { status: number}) {
    return (
    <>
        <h1>{status}</h1>
        <p>{MESSAGES[status] ?? 'Une erreur est survenue.'}</p>
        <a href="/">Retour à l'accueil</a>
    </>
    )
}

export default Erreur
