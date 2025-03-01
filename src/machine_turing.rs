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
    ribbon: Ribbon, // That modelize the ribbons of the Machine of Turing
    states: Vec<State>,
    current_state: String,
    transitions: HashMap<String,Vec<Transition>>
}

#[derive(Debug)]
pub struct MachineTuring {
    pub configuration: Configuration,
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
    pub  fn new(ribbon: Ribbon,states: Vec<State>,current_state: String,
        transitions: HashMap<String,Vec<Transition>>) -> Self {
        Self { ribbon: ribbon, states: states, current_state: current_state, transitions: transitions }
    }

    pub fn get_ribbon(&self) -> &Ribbon {
        &self.ribbon
    }
    
    pub fn get_mut_ribbon(&mut self) -> &mut Ribbon {
        &mut self.ribbon
    }

    pub fn get_transitions(&self) -> Option<&Vec<Transition>> {
        self.transitions.get(&self.current_state)
    }

    pub fn update(&mut self) -> Result<(), ()> {
        let transitions = match self.get_transitions() {
            Some(trans) => trans.clone(),
            None => return Err(()),
        };
    
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
    pub fn new(configuration:Configuration) -> Self {
        Self { configuration: configuration, step: 0u64 }
    }

    pub fn run(&mut self) -> Result<(),()> {
        let mut active = true;
        while active {
            if let Err(_) = self.configuration.update().clone() {
                active = false;
            }
        }
        self.check_final_state()
    }

    pub fn run_with_limit(&mut self, limit:u64) -> Result<(),()> {
        let mut active = true;
        while active && self.step<limit {
            if let Err(_) = self.configuration.update().clone() {
                active = false;
            }
            else {
                self.step += 1;
            }
        }
        self.check_final_state()
    }

    pub fn check_final_state(&self) -> Result<(),()> {
        let states = self.configuration.states.clone();
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