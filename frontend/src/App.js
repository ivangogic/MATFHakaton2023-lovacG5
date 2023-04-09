import React, { memo, useEffect, useState } from 'react';
import StackMemoryPage from './StackMemoryPage';
import HeapMemoryPage from './HeapMemoryPage';
import './App.css';
import {useRef} from "react";
import Xarrow from "react-xarrows";
let stackComponentsCounter = 0;

function App() {
  const [inputValue, setInputValue] = useState('');
  const [allStates, setAllStates] = useState(null);
  const [memory, setMemory] = useState(null);
  const [names, setNames] = useState(null);
  const [heap, setHeap] = useState(null);
  const [line, setLine] = useState(null);
  const [stateCount, setStateCount] = useState(-1); //current state count
  const [state, setState] = useState(null);
  const [mapping, setMapping] = useState(new Map());
  const [mappingVector, setMappingVector] = useState([]);

  const [id] = React.useState(() => {
    stackComponentsCounter += 1;
    return stackComponentsCounter;
  });
  const handleSubmit = async (e) => {
    e.preventDefault();
    const url = `http://localhost:8000/get_data?_text=${encodeURIComponent(inputValue)}`;
    const res = await fetch(url);
    const data = await res.json();
    
    setAllStates(data);
  };
  const generateKey = (pre) => {
    return `${ pre }_${ new Date().getTime() }`;
  }


  useEffect(() => {  
    if (allStates !== undefined && allStates !== null) {
      setState(allStates[stateCount]);
    }
  },[stateCount]);

  useEffect(() => {  
    setMappingVector([]);
    mapping.forEach((value, key) => {
      setMappingVector([...mappingVector, [key, value]]);
    })
  },[mapping]);

  useEffect(() => {  
    if (allStates !== undefined && allStates !== null) {
      setStateCount(0);
    }
  },[allStates]);

  useEffect(() => {  
    if(names !== undefined && names !== null){
      let newMapping = new Map()
      for (const key of Object.keys(names)) {
        let addr = names[key][0];
        let is_ptr = names[key][1];
        if(is_ptr){
          newMapping.set("memoryPage"+addr, "memoryPage"+memory[addr]);
        }
      }
      setMapping(newMapping);
    }
  },[memory]);

  useEffect(() => {  
    if (state !== undefined && state !== null) {
      setMemory(state[0]);
      setNames(state[1]);
      setHeap(state[2]);
      setLine(state[3]);
    }
    
  },[state]);

  const handleNext =()=>{
    if(stateCount + 1 < allStates.length){
      setStateCount(stateCount+1);
    }
  };

  const handlePrev =()=>{
    if(stateCount - 1 >= 0){
      setStateCount(stateCount-1);
    }
  };

  return (
    <div className="container">
      <div className="code_column">
        <h3 className="input_code">Input Code</h3>
        <form onSubmit={handleSubmit}>
          <textarea className="code_textarea"
            rows={20}
            value={inputValue}
            style={{}}
            onChange={(e) => setInputValue(e.target.value)}
          />
          
        </form>
        <div className="buttons">
          <button type="button" className="button" onClick={handlePrev}>
            Prev
          </button>
          <button type="submit" onClick={handleSubmit} className="button">
            Evaluate
          </button>
          <button type="button" className="button" onClick={handleNext}>
            Next
          </button>
        </div>
      </div>
      <div className="memory_column">
        <div className="memory_stack">
          {names ? (
            Object.keys(names).map(key=>(
              <StackMemoryPage id={"memoryPage"+names[key][0]} key={key} variable_name = {key} type = {names[key][2]} is_pointer = {names[key][1]}
              address = {names[key][0]}
              value = {names[key][1] ? names[key][0] : memory[names[key][0]]}/>
            ))
          ) : (null)
          }
        </div>
        <div className="memory_heap">
          {memory ? (
            Object.keys(memory).map(key=>(
              key >= 2000 ? 
              <HeapMemoryPage id={"memoryPage"+key} key={key} 
              address = {key}
              value = {memory[key]}
              />
              :
              null
            ))
            ) : (null)
          }
        </div>
      </div>
      <div className='thirdcolumn'>
        {Array.from(mapping).map(([key, value]) => {
                  if (value.substring(10,14) in memory) {
                    return <Xarrow key={key + "->" + value} start={key} end={value} />;
                  } else {
                    return  <Xarrow key={key + "->" + "memoryPageNonExistant"} start={key} end="memoryPageNonExistant"/>;                    
                  }
                }
        )}
      </div>
    </div>
  );
}

export default App;
