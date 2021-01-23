# coda (covid-19 data for all)

A large amount of scientific literature (reports, articles, case studies) and data regarding COVID-19 is already available – for example, browse COVID-19 Pandemic in Europe, WHO COVID-19 Dashboard, Coronavirus @ Worldometer, medRxiv, BMJ's Coronavirus Hub, COVID-19 Open Data. Create a "smart" (micro-)service-based Web system able to provide for both specialists and general public support for studying, visualizing, annotating, augmenting, and sharing – in multiple formats – the most authoritative and useful knowledge about this disease, including important advices, regional statistics, evolution & prediction. Implement at least three of the enumerated services. All processed data/knowledge will be accessed via a SPARQL endpoint – a useful ontology: CIDO (Coronavirus Infectious Disease Ontology). Inspiration: A knowledge-graph platform for newsrooms. Additional resources: COVID-19 Developer Resource Center. Bonus: capturing and exposing useful provenance.


ontology:
```
Cases
| Property                | Expected Type             | Description                                                                                               |
| ----------------------- | ------------------------- | --------------------------------------------------------------------------------------------------------- |
| rdf:type                |  OWL.Class                | A blank node                                                                                              |
| rdfs:subClassOf         |  OWL.Thing                | is a thing                                                                                                |
| ns1:IsReportedOn        |  Literal (xsd:dateTime)   | is a thing                                                                                                |
| ns1:IsOfType            |  Literal (string)         | is a thing                                                                                                |
| ----------------------- | ------------------------- | --------------------------------------------------------------------------------------------------------- |






```