CREATE_ENTITY_URL = 'http://10.53.164.216:31550/graphql'
LOGIN_REQUEST_URL = 'http://10.53.164.216:31831/login/handle/LoginRequest'
CREATE_PHONE_QUERY = "mutation createEntity($entity: createNewEntityInputType, $remarks: [remarkInput], $classification: String $tags: [String!], $links : [LinkBaseType]) {response: entitiesMutation {createEntity(createEntityInput: $entity) {entityId setLinks(setLinkBaseType: {links: $links}) setClassification(classification: $classification) addRemarks(createRemarks: {remarks: $remarks}) { id } setTags(setTags: $tags)}}}"
CREATE_VEHICLE_QUERY = "mutation createEntity($entity: createNewEntityInputType, $remarks: [remarkInput], $classification: String  $tags: [String!],$links : [LinkBaseType]) {response: entitiesMutation {createEntity(createEntityInput: $entity) {entityId setLinks(setLinkBaseType: {links: $links}) setClassification(classification: $classification) addRemarks(createRemarks: {remarks: $remarks}) { id } setTags(setTags: $tags)}}}"
CREATE_NEWS_QUERY = "mutation saveNewsDraft($newsDraft: newsItemDraftInputType!, $newsDraftId: String!, $classificationId: String!, $tags: [String], , $links: [LinkBaseType!]){  newsItem{    updateDraft(newsItemDraft: $newsDraft){      body        priorityEnumId        reliabilityEnumId        sourceEnumId        sourceName        sourceCredibilityEnumId        subject        typeEnumId        crimeTypeEnumIds        occurrenceTime {          startTime          endTime        }        id        locations{          address{            floor            state            colony            street            postalCode            country            district            settlement            description            neighborhood            externalNumber            internalNumber            apartmentNumber          }          addressMeta{            country            state            district            settlement            street            externalNumber          }          time{            from            to          }          description          locationGeometries{            point{              type              coordinates            }            polygon{              type              coordinates            }            description          }      }    }  }  permissions{  setClassification(setClassificationInput: {classification: $classificationId, entityId: $newsDraftId})}tags{  setTags(setTagsInput:{entityId: $newsDraftId,tagEnumIds: $tags}){    tagEnumId  }}links {  setLinks(setLinkBaseType: {links: $links, sourceId: $newsDraftId})}}"
ACTIONS_TEMPLATES = {
    1: {
        "template": "create_entity_template.json",
        "query": CREATE_PHONE_QUERY
    },
    2: {
        "entity": "create_entity_template.json",
        "query": CREATE_VEHICLE_QUERY
    },
    3: {
        "entity": "create_news_template.json",
        "query": CREATE_NEWS_QUERY
    }
}