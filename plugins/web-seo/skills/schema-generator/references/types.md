# Schema templates

Replace every value. Keep `@id`s stable across pages: the same business is always `https://example.com/#business`.

## Graph for a page (default for new sites)

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "WebSite", "@id": "https://example.com/#website", "url": "https://example.com/", "name": "Site name", "inLanguage": "es" },
    { "@type": "Plumber", "@id": "https://example.com/#business", "...": "see LocalBusiness" },
    { "@type": "WebPage", "@id": "https://example.com/page/#webpage", "url": "https://example.com/page/", "name": "Page title", "isPartOf": { "@id": "https://example.com/#website" }, "about": { "@id": "https://example.com/#business" } }
  ]
}
```

## LocalBusiness (use the most specific subtype)

Common subtypes: `Plumber`, `Electrician`, `HVACBusiness`, `AutoRepair`, `BikeStore` / `SportingGoodsStore`, `LodgingBusiness` (`Hotel`, `Apartment` for rentals), `ProfessionalService`.

```json
{
  "@type": "Plumber",
  "@id": "https://example.com/#business",
  "name": "Business name",
  "url": "https://example.com/",
  "telephone": "+44XXXXXXXXXX",
  "email": "hello@example.com",
  "description": "One or two sentences that match the site.",
  "image": "https://example.com/og-image.jpg",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "…",
    "addressLocality": "…",
    "postalCode": "…",
    "addressCountry": "GB"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": 0, "longitude": 0 },
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "08:00", "closes": "18:00" }
  ],
  "areaServed": [
    { "@type": "City", "name": "Brighton" },
    { "@type": "City", "name": "Hove" }
  ],
  "sameAs": []
}
```

- Service-area businesses with no public address: keep `areaServed`, leave the street address out instead of inventing one.
- `geo` only with real coordinates.

## Service

```json
{
  "@type": "Service",
  "@id": "https://example.com/services/boiler-repair/#service",
  "name": "Boiler repair",
  "serviceType": "Boiler repair",
  "description": "…",
  "provider": { "@id": "https://example.com/#business" },
  "areaServed": { "@type": "City", "name": "Brighton" }
}
```

Add `offers` only when the page shows a price.

## FAQPage

```json
{
  "@type": "FAQPage",
  "@id": "https://example.com/page/#faq",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Question exactly as on the page?",
      "acceptedAnswer": { "@type": "Answer", "text": "Answer exactly as on the page." }
    }
  ]
}
```

Only questions and answers that are visible on the page.

## Person and Organization (personal and studio sites)

```json
{ "@type": "Person", "@id": "https://example.com/#person", "name": "…", "url": "https://example.com/", "jobTitle": "…", "worksFor": { "@id": "https://studio.example/#organization" }, "sameAs": [] }
```

When two sites share one person or company, use the same `@id` on both (the canonical site's URL) and link to it instead of redefining it.

## Mistakes to avoid

- `LocalBusiness` when a subtype exists.
- Missing `@id`, or a different `@id` for the same entity on different pages.
- Values the page doesn't show, or invented values.
- Plain-string `areaServed` when a typed place fits.
- Mixing a graph and separate blocks on the same site.
