import { useState } from 'react'
import { post, type User, type List_Service} from '../../api.ts'


function Listing_services({ array_services}: { array_services: List_Service[] }) {
    return (
        array_services.map((element) => (
            <h3 key={element.id}>{element.name}</h3>
            <
        ))
    )
}