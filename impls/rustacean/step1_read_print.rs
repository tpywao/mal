#[macro_use]
extern crate lazy_static;
extern crate itertools;

extern crate rustyline;
use rustyline::error::ReadlineError;
use rustyline::Editor;

#[macro_use]
mod types;
mod reader;
mod printer;

fn main() {
  let mut rl = Editor::<()>::new();

  loop {
    let readline = rl.readline("user> ");
    match readline {
      Ok(line) => {
        if line.len() > 0 {
          match reader::read_str(line) {
            Ok(ast) => println!("{}", ast.pr_str()),
            Err(e) => println!("{:?}", e),
          }
        }
      },
      Err(ReadlineError::Interrupted) => continue,
      Err(ReadlineError::Eof) => break,
      Err(err) => {
        println!("Error: {:?}", err);
        break;
      },
    }
  }
}