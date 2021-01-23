# coda (covid-19 data for all)

A large amount of scientific literature (reports, articles, case studies) and data regarding COVID-19 is already available – for example, browse COVID-19 Pandemic in Europe, WHO COVID-19 Dashboard, Coronavirus @ Worldometer, medRxiv, BMJ's Coronavirus Hub, COVID-19 Open Data. Create a "smart" (micro-)service-based Web system able to provide for both specialists and general public support for studying, visualizing, annotating, augmenting, and sharing – in multiple formats – the most authoritative and useful knowledge about this disease, including important advices, regional statistics, evolution & prediction. Implement at least three of the enumerated services. All processed data/knowledge will be accessed via a SPARQL endpoint – a useful ontology: CIDO (Coronavirus Infectious Disease Ontology). Inspiration: A knowledge-graph platform for newsrooms. Additional resources: COVID-19 Developer Resource Center. Bonus: capturing and exposing useful provenance.


### CODA - Used Vocabulary

```text
| -------------------------------------------------------------------------------------------------------- |
| Class Name: Country                                                                                      |
| -------------------------------------------------------------------------------------------------------- |
| URI                       |  http://coda.org/resources/countries                                         |
| Definition                |  A country, identified by its ISO(alpha 2) code                              |
| Type of term              |  Class                                                                       |
| Subclass of               |  https://schema.org/Country                                                  |
| -------------------------------------------------------------------------------------------------------- |
| -------------------------------------------------------------------------------------------------------- |
| Property Name: IdentifiedBy                                                                              |
| -------------------------------------------------------------------------------------------------------- |
| URI                       |  http://coda.org/resources/properties/IdentifiedBy                           |
| Definition                |  A related resource that uniquely identifies the described resource          |
| Type of term              |  Property                                                                    |
| Used on types             |  Country, News, Article                                                      |
| -------------------------------------------------------------------------------------------------------- |
| -------------------------------------------------------------------------------------------------------- |
| Property Name: hasCases                                                                                  |
| -------------------------------------------------------------------------------------------------------- |
| URI                       |  http://coda.org/resources/properties/hasCases                               |
| Definition                |  Associates a case node to a country                                         |
| Type of term              |  Property                                                                    |
| Used on types             |  Country                                                                     |
| -------------------------------------------------------------------------------------------------------- |
| -------------------------------------------------------------------------------------------------------- |
| Class Name: Cases                                                                                        |
| -------------------------------------------------------------------------------------------------------- |
| URI                       |  -                                                                           |
| Definition                |  A BNode containing the cases recorded in a day for a country                |
| Type of term              |  Class                                                                       |
| Subclass Of               |  https://www.w3.org/2002/07/owl#Thing                                        |
| -------------------------------------------------------------------------------------------------------- |
| -------------------------------------------------------------------------------------------------------- |
| Property Name: value                                                                                     |
| -------------------------------------------------------------------------------------------------------- |
| URI                       |  https://www.w3.org/1999/02/22-rdf-syntax-ns#value                           |
| Definition                |  Number of cases of the specified type                                       |
| Type of term              |  Propery                                                                     |
| Used on types             |  Cases                                                                       |
| -------------------------------------------------------------------------------------------------------- |
| -------------------------------------------------------------------------------------------------------- |
| Property Name: IsOfType                                                                                  |
| -------------------------------------------------------------------------------------------------------- |
| URI                       |  http://coda.org/resources/properties/IsOfType                               |
| Definition                |  Type of case; one of (total_)confirmed, (total_)recovered,                  |
|                           |  (total_)deceased, active                                                    |
| Type of term              |  Property                                                                    |
| Used on types             |  Cases                                                                       |
| -------------------------------------------------------------------------------------------------------- |
| -------------------------------------------------------------------------------------------------------- |
| Property Name: IsReportedOn                                                                              |
| -------------------------------------------------------------------------------------------------------- |
| URI                       |  http://coda.org/resources/properties/IsReportedOn                           |
| Definition                |  Date when the cases occurred (ISO format)                                   |
| Type of term              |  Property                                                                    |
| Used on types             |  Cases                                                                       |
| -------------------------------------------------------------------------------------------------------- |
| -------------------------------------------------------------------------------------------------------- |
| Class Name: News                                                                                         |
| -------------------------------------------------------------------------------------------------------- |
| URI                       |  http://coda.org/resources/news                                              |
| Definition                |  News related to COVID-19                                                    |
| Type of term              |  Class                                                                       |
| Subclass of               |  https://schema.org/NewsArticle                                              |
| -------------------------------------------------------------------------------------------------------- |
| -------------------------------------------------------------------------------------------------------- |
| Property Name: PublishedIn                                                                               |
| -------------------------------------------------------------------------------------------------------- |
| URI                       |  http://coda.org/resources/properties/IsReportedOn                           |
| Definition                |  Publication / website where the news was posted                             |
| Type of term              |  Property                                                                    |
| Used on types             |  News                                                                        |
| -------------------------------------------------------------------------------------------------------- |
| -------------------------------------------------------------------------------------------------------- |
| Property Name: urlSource                                                                                 |
| -------------------------------------------------------------------------------------------------------- |
| URI                       |  https://schema.org/url                                                      |
| Definition                |  URL of the news source                                                      |
| Type of term              |  Property                                                                    |
| Used on types             |  News, Articles                                                              |
| -------------------------------------------------------------------------------------------------------- |
| -------------------------------------------------------------------------------------------------------- |
| Property Name: datePublished                                                                             |
| -------------------------------------------------------------------------------------------------------- |
| URI                       |  https://schema.org/datePublished                                            |
| Definition                |  Date of first publication                                                   |
| Type of term              |  Property                                                                    |
| Used on types             |  News, Articles                                                              |
| -------------------------------------------------------------------------------------------------------- |
| -------------------------------------------------------------------------------------------------------- |
| Property Name: headline                                                                                  |
| -------------------------------------------------------------------------------------------------------- |
| URI                       |  https://schema.org/headline                                                 |
| Definition                |  News headline / title                                                       |
| Type of term              |  Property                                                                    |
| Used on types             |  News, Articles                                                              |
| -------------------------------------------------------------------------------------------------------- |
| -------------------------------------------------------------------------------------------------------- |
| Property Name: keywords                                                                                  |
| -------------------------------------------------------------------------------------------------------- |
| URI                       |  https://schema.org/keywords                                                 |
| Definition                |  Keywords or tags used to describe the news (delimited by commas)            |
| Type of term              |  Property                                                                    |
| Used on types             |  News                                                                        |
| -------------------------------------------------------------------------------------------------------- |
| -------------------------------------------------------------------------------------------------------- |
| Property Name: imgURL                                                                                    |
| -------------------------------------------------------------------------------------------------------- |
| URI                       |  http://coda.org/resources/properties/imgURL                                 |
| Definition                |  URL to the image posted with this news                                      |
| Type of term              |  Property                                                                    |
| Used on types             |  News                                                                        |
| -------------------------------------------------------------------------------------------------------- |
| -------------------------------------------------------------------------------------------------------- |
| Class Name: Articles                                                                                     |
| -------------------------------------------------------------------------------------------------------- |
| URI                       |  http://coda.org/resources/articles                                          |
| Definition                |  A research article related to COVID-19                                      |
| Type of term              |  Class                                                                       |
| Subclass of               |  https://schema.org/ScholarlyArticle                                         |
| -------------------------------------------------------------------------------------------------------- |
| -------------------------------------------------------------------------------------------------------- |
| Property Name: hasType                                                                                   |
| -------------------------------------------------------------------------------------------------------- |
| URI                       |  http://coda.org/resources/properties/hasType                                |
| Definition                |  Type of article; one of: article, journal contribution, dataset             |
| Type of term              |  Property                                                                    |
| Used on types             |  Articles                                                                    |
| -------------------------------------------------------------------------------------------------------- |
| -------------------------------------------------------------------------------------------------------- |
| Property Name: about                                                                                     |
| -------------------------------------------------------------------------------------------------------- |
| URI                       |  https://schema.org/about                                                    |
| Definition                |  The subject matter of the content.                                          |
| Type of term              |  Property                                                                    |
| Used on types             |  Articles                                                                    |
| -------------------------------------------------------------------------------------------------------- |
| -------------------------------------------------------------------------------------------------------- |
| Property Name: abstract                                                                                  |
| -------------------------------------------------------------------------------------------------------- |
| URI                       |  https://schema.org/abstract                                                 |
| Definition                |  Short description that summarizes an article                                |
| Type of term              |  Property                                                                    |
| Used on types             |  Articles                                                                    |
| -------------------------------------------------------------------------------------------------------- |
| -------------------------------------------------------------------------------------------------------- |
| Property Name: author                                                                                    |
| -------------------------------------------------------------------------------------------------------- |
| URI                       |  https://schema.org/author                                                   |
| Definition                |  The author of this article                                                  |
| Type of term              |  Property                                                                    |
| Used on types             |  Articles                                                                    |
| -------------------------------------------------------------------------------------------------------- |
| -------------------------------------------------------------------------------------------------------- |
```




