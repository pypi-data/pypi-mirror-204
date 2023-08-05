from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import cimgraph.data_profile.rc4_2021 as cim


def get_all_attributes(feeder_mrid: str, typed_catalog: dict[type, dict[str, object]]) -> str: 
    """ Generates SPARQL query string for a given catalog of objects and feeder id
    Args:
        feeder_mrid (str | Feeder object): The mRID of the feeder or feeder object
        typed_catalog (dict[type, dict[str, object]]): The typed catalog of CIM objects organized by 
            class type and object mRID
    Returns:
        query_message: query string that can be used in blazegraph connection or STOMP client
    """

    mrid_list = list(typed_catalog[cim.Terminal].keys())

    
    query_message = """
        PREFIX r:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX cim:  <http://iec.ch/TC57/CIM100#>
        SELECT ?mRID ?name ?connected ?sequenceNumber ?OperationalLimitSet ?ConductingEquipment ?TransformerEnd
        ?ConnectivityNode ?TopologicalNode ?RegulatingControl
        (group_concat(distinct ?Measurement; separator=";") as ?Measurements) 
        WHERE {          
          ?eq r:type cim:Terminal.
          VALUES ?fdrid {"%s"}
          VALUES ?mRID {"""%feeder_mrid
    # add all equipment mRID
    for mrid in mrid_list:
        query_message += ' "%s" \n'%mrid
    # add all attributes
    query_message += """               } 
        #get feeder id from connectivity node
        ?eq cim:Terminal.ConnectivityNode ?cn.
        ?cn cim:ConnectivityNode.ConnectivityNodeContainer ?fdr.
        ?fdr cim:IdentifiedObject.mRID ?fdrid.
        
        ?eq cim:IdentifiedObject.mRID ?mRID.
        ?eq cim:IdentifiedObject.name ?name.
        
        OPTIONAL {?eq cim:ACDCTerminal.connected ?connected.}
        OPTIONAL {?eq cim:ACDCTerminal.sequenceNumber ?sequenceNumber.}
        OPTIONAL {?eq cim:ACDCTerminal.OperationalLimitSet ?oplim.
                  ?oplim cim:IdentifiedObject.mRID ?OperationalLimitSet.}
        
        OPTIONAL {?eq cim:Terminal.ConductingEquipment ?coneq.
                  ?coneq cim:IdentifiedObject.mRID ?ConductingEquipment.}
        OPTIONAL {?xfmr cim:TransformerEnd.Terminal ?eq.
                  ?xfmr cim:IdentifiedObject.mRID ?TransformerEnd.}
        
        ?cn cim:IdentifiedObject.mRID ?ConnectivityNode.
        OPTIONAL {?cn cim:ConnectivityNode.TopologicalNode ?topo.
                  ?topo cim:IdentifiedObject.mRID ?TopologicalNode.}
        
        OPTIONAL {?regcntrl cim:RegulatingControl.Terminal ?eq.
                  ?regcntrl cim:IdentifiedObject.mRID ?RegulatingControl.}
        
        OPTIONAL {?meas cim:Measurement.Terminal ?eq.
          ?meas cim:IdentifiedObject.mRID ?Measurement}

        }
        GROUP BY  ?mRID ?name ?connected ?sequenceNumber ?OperationalLimitSet ?ConductingEquipment 
        ?TransformerEnd ?ConnectivityNode ?TopologicalNode ?RegulatingControl
        ORDER by  ?name 
    """

    return query_message
