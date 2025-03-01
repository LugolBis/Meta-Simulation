#[derive(Debug)]
struct Configuration {
    ribbon: String,
    transitions: String 
}

#[derive(Debug)]
struct CellularAutomata {
    configuration: Configuration,
    stage: u64
}