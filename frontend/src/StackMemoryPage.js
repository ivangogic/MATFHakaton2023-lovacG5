import './MemoryPage.css';
import React, { useState } from 'react';

export function StackMemoryPage(props){
    
    return (
        <div id = {props.id} className="memory_page">
            <div className="memory_address">
                <h4>{props.address}: </h4>
            </div>
            <div className="memory_content">
                <h4>
                    {
                        props.is_pointer ?
                        props.variable_name + ": " + props.type :
                        props.variable_name + " : " + props.value 
                    }
                </h4>
            </div>
        </div>
    )
}

export default StackMemoryPage