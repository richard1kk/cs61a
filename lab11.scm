(define (if-program condition if-true if-false)
  `(if ,condition ,if-true ,if-false)
)


(define (square n) (* n n))

(define (pow-expr base exp) 
  (cond ((= exp 0) 1)
        ((= exp 1) `(* ,base ,exp))
        ((even? exp) `(square ,(pow-expr base (/ exp 2))))
        ((odd? exp) `(* ,base ,(pow-expr base (- exp 1))))
    )
)  


(define-macro (repeat n expr)
  `(repeated-call ,n (lambda () ,expr)))

; Call zero-argument procedure f n times and return the final result.
(define (repeated-call n f)
  (if (= n 1)
      (f)
      (begin (f) (repeated-call (- n 1) f))))

; cons creates another set of paranthesese around
; Macros: created using define-macro.
; 1. Binding formal parameters of macro to unevaluated operands expressions
; 2. Evaluate body of macro, returns an expression
; 3. Evaluate expression returned by macro in frame of original macro call
; 
