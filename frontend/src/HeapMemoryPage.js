import './MemoryPage.css';


export function HeapMemoryPage(props){
    return (
        <div id = {props.id}  ref={props.ref} className="memory_page">
            <div className="memory_address">
                <h4>{props.address}: </h4>
            </div>
            <div className="memory_content">
                <h4>{props.is_pointer ? '*' : (null)}{props.variable_name} = {props.value}</h4>
            </div>
        </div>
    )
}

export default HeapMemoryPage