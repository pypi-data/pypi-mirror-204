# Error Handling

!!! note "Happy 😀 vs unhappy 🫠 path"
    When we write software we tend to only think in the **happy path**, the flow the software will go through in the default scenario featuring no exceptional or error conditions. Happy path test is a well-defined test case using known input, which executes without exception and produces and expected output. Happy path testing can show that a system meets its functional requirements but it doesn't guarantee a graceful handling of error conditions or aid in fiding hidden bugs.

    In use case analysis, there is only one happy path, but there may be any number of additional alternate path scenarions which are all valid optional outcomes. If valid alternatives exist, the happy path is then identified as the default or most likely positive alternative. The analysis may also show one or more exception paths. An exception path is takes as result of a fault condition.

!!! note "`Result` typing and error handling inspired in `rust-lang`"
    Modern languages like `rust` and `go` have a completely different ways to propagate errors, compared to languages like `python`, `java` or `javascript`. In the last, you'd basically raise or throw and exceptions and then wrap whatever code may failed between a `try/except` or `try/catch` clause.

    In constrast, `rust` and `go` both implement something different. Not deterministic[^1] code will return both the result of the code execution or an error associated with the failure of the code execution. That's why you would see code like this many times when reading code base on this languages.
    

    ```go
    f, err := os.Open("filename.txt")
    if err != nil {
        log.Fatal(err) // handled error
    }
    // continue
    ```


    ```rust
    let file = File::open("main.jpg");
    let file_err = file.as_ref().err();
    if file_err.is_some() {
        println!("File not found!") // handled error
    }
    // continue
    ```

    The greatest advantage for software developers for this type of error propagation system is that error are also part of the typing annotation of the functions. So whoever is calling that piece of code, is required to propery handled failure cases if not the compiler will cry. (Or the `static type checker` in case of Python.)

    Another advantage is that languages like `rust` and `go` separate errors in two categories:
    - Non-Recoverable Errors (e.g., non-checked out of bounds array access.)
    - Recoverable Errors (e.g., function failures.)

    By definition, `Non-Recoverable Errors` will crash your system while `Recoverable Errors` are propagated to the client to be propertly handled. But the system won't break because of those.

[^1]: A deterministic code is a code that, given a certain input, will always return produce the same output, with the underlaying machine always passing throw the same sequence of steps. Formally, a deterministic algorithm computes a *mathematical function*; a function has a unique value for any input in its domain, and the algorithm is a process that produces this particular value as output. In contrast, a non deterministic code is code that, for a variety of factors, can cause an algorithm to behave in a way which is not expected.