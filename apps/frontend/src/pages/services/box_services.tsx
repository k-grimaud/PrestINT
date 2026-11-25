import { type List_Service } from '../../api.ts'

function Listing_services({ array_services }: { array_services: List_Service[] }) {
    return (
        array_services.map((element) => (
            <h3 key={element.list_service_id}>{element.name}</h3>
        ))
    )
}

export default Listing_services
