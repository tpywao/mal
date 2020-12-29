extern crate rustyline;
use rustyline::error::ReadlineError;
use rustyline::Editor;

fn main () {
  let mut rl = Editor::<()>::new();

  loop {
    let readline = rl.readline("user> ");
    match readline {
      Ok(line) => {
        if line.len() > 0 {
          println!("{}", line);
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