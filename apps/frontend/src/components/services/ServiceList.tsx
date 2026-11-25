import { type List_Service } from '../../api.ts'

function ServiceList({ services }: { services: List_Service[] }) {
  if (services.length === 0) {
    return <p>Aucune prestation trouvée</p>
  }

  return (
    <section className="boxes">
      {services.map((service) => (
        <div key={service.list_service_id}>
          <h3>{service.name}</h3>
          <p>Club : {service.asso_id}</p>
          <p>{service.description}</p>
          <p>Prix : {service.approximative_cost}</p>
          <p>Durée : {service.approximative_time}</p>
        </div>
      ))}
    </section>
  )
}

export default ServiceList