export interface ClubsData {
    name: string;
    type: string;
    affiliation?: string;
    logo: string;
    description: string;
    links: string[];
}

export const members: ClubsData[] = [{
    name: "BDA",
    type: "Asso",
    logo: "/.../logo_bda.png",
    description: "description...",
    links: ["https://bda-imtbs-tsp.fr/clubs"],
}
];