;The first program

(begin
    (display "Hello, World!")
    ;1.2
    (define x (+ (+ 5 4)
                 (- 2 
                    (- 3
                        (+  6 
                            (/ 4 5)))))
    )
    (define y (* (* 3 
                    (- 6 2))
                 (- 2
                    7))
    )
    (define result (/ x y))
    
    ;1.3
    (define (max_two_add x y z)
            (cond ((> (+ x y) (+ x z)) 
                        (cond((> (+ x y) (+ y z)) (+ x y))
                            (else (+ y z))))
                (else (cond((> (+ x z) (+ y z)) (+ x z))
                        (else (+ y z)))
                )
            ))
    ;max
    
    (define (max x_ y_ z_) 
        (cond ((> x_ y_)
                (cond ((> x_ z_) x_)
                     (else z_)))
             ((<= x_ y_)
                (cond ((> y_ z_) y_)
                      (else z_)
                      ))
            ;  (else x_)         
                    )
        )

        ; (define (<= x y)
        ; (or (< x y) (= x y)))
    (define (xxx a b c)
        (cond ((and (<= a b) (<= a c))   c)
                 ((and (<= b a) (<= b c))   (+ a c))
                 (else              
                                       (+ a b))))
    ;实例1.17 牛顿求根法
    (define (new-if p g x)
            (cond ((p) g)
             (else x)))

    (define (sqrt guess x)
            ( new-if (sqrt_cond guess (sqrt (/ (+ 
                               (/ x guess)
                                guess)
                            2) 
                                x))))


            ; (if (sqrt_cond guess x) 
            ;     guess
            ;     (sqrt (/ (+ 
            ;                (/ x guess)
            ;                 guess)
            ;             2) 
            ;                 x)))
    
    (define (sqrt_cond guess x)
            (< (abs(- (* guess guess) x)) 0.00000000000001))
    
    ;  (((y/g)+g)/2**2 -y)<value
    ;1.6 重新定义 正则序 (完全展开后归约) ：正则序的递归 会陷入死循环
    (newline))
    ;3(6-2)(2-7)