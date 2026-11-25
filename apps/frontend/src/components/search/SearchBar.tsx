function SearchBar({ value, onChange }: { value: string; onChange: (v: string) => void }) {
  return (
    <input
      className="search"
      type="text"
      placeholder="Rechercher une prestation ou un club"
      value={value}
      onChange={(e) => onChange(e.target.value)}
    />
  )
}

export default SearchBar