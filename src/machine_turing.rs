use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct State(pub String, pub bool);

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Value {
    Empty,
    Text(String)
}

#[derive(Debug, Clone)]
pub enum MoveTo {
    Right,
    Left,
    Stay
}

#[derive(Debug,Clone)]
pub struct Ribbon {
    head: usize,
    value: Vec<Value>
}

#[derive(Debug, Clone)]
pub struct Transition {
    read: Value,
    write: Value,
    movement: MoveTo,
    futur_state: String
}

#[derive(Debug)]
pub struct Configuration {
    ribbon: Ribbon, // That modelize the ribbon of the Machine of Turing
    current_state: String,
}

#[derive(Debug)]
pub struct MachineTuring {
    pub configuration: Configuration,
    pub states: Vec<State>,
    pub transitions: HashMap<String,Vec<Transition>>,
    pub step: u64
}

impl State {
    pub fn from(name:&str, accept:bool) -> Self {
        Self(String::from(name), accept)
    }
}

impl Value {
    pub fn from(value: &str) -> Self {
        match value {
            "" => Value::Empty,
            _ => Value::Text(String::from(value))
        }
    }
}

impl Ribbon {
    pub fn from(input: Vec<&str>) -> Self {
        Self { head: 0usize, value: input.iter().map(|c| Value::Text(String::from(*c))).collect() }
    }

    pub fn get(&self) -> &Value {
        &self.value[self.head]
    }

    pub fn set(&mut self, new_value: Value) {
        self.value[self.head] = new_value;
    }

    pub fn left(&mut self) {
        if self.head == 0 { todo!(); }
        else { self.head -= 1; }
    }

    pub fn right(&mut self) {
        if self.head == self.value.len()-1 { self.value.push(Value::Empty); self.head += 1; }
        else { self.head += 1; }
    }
}

impl Transition {
    pub fn from(read:&str,write:&str,movement:MoveTo,futur_state:&str) -> Self {
        Self { read: Value::from(read), write: Value::from(write), movement: movement, futur_state: String::from(futur_state) }
    }
}

impl Configuration {
    pub  fn new(ribbon: Ribbon,current_state: String) -> Self {
        Self { ribbon: ribbon, current_state: current_state }
    }

    pub fn get_ribbon(&self) -> &Ribbon {
        &self.ribbon
    }
    
    pub fn get_mut_ribbon(&mut self) -> &mut Ribbon {
        &mut self.ribbon
    }

    pub fn get_current_state(&self) -> String {
        String::from(&self.current_state)
    }

    pub fn update(&mut self, transitions:Vec<Transition>) -> Result<(), ()> {   
        let ribbon = self.get_mut_ribbon();
        for transition in transitions {
            if transition.read == *ribbon.get() {
                ribbon.set(transition.write.clone());
                match transition.movement {
                    MoveTo::Left => ribbon.left(),
                    MoveTo::Right => ribbon.right(),
                    MoveTo::Stay => {}
                }
                self.current_state = transition.futur_state;
                return Ok(());
            }
        }
        Err(())
    }
}

impl MachineTuring {
    pub fn new(configuration:Configuration, states:Vec<State>, transitions:HashMap<String,Vec<Transition>>) -> Self {
        Self { configuration: configuration, states: states, transitions: transitions, step: 0u64 }
    }

    pub fn get_transitions(&self) -> Option<Vec<Transition>> {
        match self.transitions.get(&self.configuration.get_current_state()) {
            Some(vector) => Some(vector.clone()),
            None => None
        }
    }

    pub fn run(&mut self) -> Result<(),()> {
        let mut active = true;
        while active {
            match self.get_transitions() {
                Some(transitions) => {
                    if let Err(_) = self.configuration.update(transitions).clone() {
                        active = false;
                    }
                }
                None => active = false
            }
            
        }
        self.check_final_state()
    }

    pub fn run_with_limit(&mut self, limit:u64) -> Result<(),()> {
        let mut active = true;
        while active && self.step<limit {
            match self.get_transitions() {
                Some(transitions) => {
                    if let Err(_) = self.configuration.update(transitions).clone() {
                        active = false;
                    }
                }
                None => active = false
            }
            
        }
        self.check_final_state()
    }

    pub fn check_final_state(&self) -> Result<(),()> {
        let states = self.states.clone();
        for state in states {
            if state.0 == self.configuration.current_state {
                if state.1 == true {
                    return Ok(());
                }
                else {
                    return Err(());
                }
            }
        }
        Err(())
    }
}

#[cfg(test)]
mod tests {
    use crate::machine_turing::*; 

    fn create_mt() -> MachineTuring {
        let ribbon = Ribbon::from(vec!["0","1","1","1"]);
        let states = vec![
            State::from("start",false),
            State::from("accept",true),
            State::from("reject",false),
            State::from("right",false),
            State::from("add",false)
        ];
        let init_state = String::from("start");
        let mut transitions: HashMap<String,Vec<Transition>> = HashMap::new();
        transitions.insert(String::from("start"), vec![
            Transition::from("", "", MoveTo::Stay, "reject"),
            Transition::from("0","0",MoveTo::Right,"right")
        ]);
        transitions.insert(String::from("right"), vec![
            Transition::from("1","1",MoveTo::Right,"right"),
            Transition::from("0","0",MoveTo::Right,"right"),
            Transition::from("", "",MoveTo::Left, "add")
        ]);
        transitions.insert(String::from("add"), vec![
            Transition::from("0","1",MoveTo::Stay,"accept"),
            Transition::from("1","0",MoveTo::Left,"add"),
            Transition::from("","1",MoveTo::Stay,"accept")
        ]);
        MachineTuring::new(Configuration::new(ribbon,  init_state),states, transitions)
    }

    #[test]
    fn test_run() {
        let mut mt = create_mt();
        match mt.run() {
            Ok(_) => println!("Successfully run the MT :\n{:?}",mt.configuration.get_ribbon()),
            Err(_) => println!("Error when run the MT :\n{:?}",mt.configuration.get_ribbon())
        }
    }

    #[test]
    fn test_run_limit() {
        let mut mt = create_mt();
        match mt.run_with_limit(10) {
            Ok(_) => println!("Successfully run the MT :\n{:?}",mt.configuration.get_ribbon()),
            Err(_) => println!("Error when run the MT :\n{:?}",mt.configuration.get_ribbon())
        }
    }
}