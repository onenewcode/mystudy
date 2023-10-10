use std::env;
use std::process;
use minigrep::Config;
use minigrep::run;
fn main() {
    // 获取命令行变量
    let args: Vec<String> = env::args().collect();
// 当 Result 是 Ok 时，这个方法的行为类似于 unwrap：它返回 Ok 内部封装的值。然而，`当其值是 Err 时，该方法会调用一个 闭包（closure）``也就是一个我们定义的作为参数传递给 unwrap_or_else 的匿名函数
    let config = Config::build(&args).unwrap_or_else(|err| {
        println!("Problem parsing arguments: {err}");
        process::exit(1);
    });

    println!("Searching for {}", config.query);
    println!("In file {}", config.file_path);
    
    if let Err(e) = run(config) {
        println!("Application error: {e}");
        process::exit(1);
    }
    
}
 