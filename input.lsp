; 이라인은 주석입니다.
; lisp 문법에 의해 newline 나오기 전까지는 주석으로 처리합니다.

; LISP의 산술연산
(+ 3 5)
(+ 3 (* 5 6))

; setq
(SETQ X 5);
X
(LIST 'X X 'Y)

; car
(CAR '(X Y Z));
(CAR '((X) Y Z))

; cdr
(CDR '(X Y Z))

; car과 cdr의 혼합
(SETQ X '(1 2 3))
(CAR (CDR (CDR X)));
(CADDR X);

; NTH
(NTH 4 '(0 1 2 3 4 5 6));
(NTH 3 '(A B));
(NTH 3 'A);

; CONS
(CONS 'A '(B C D));

; REVERSE
(REVERSE '(A B C D));

; APPEND
(APPEND '(A C) '(B D) '(E F));

; LENGTH
(LENGTH '(A B C));
(LENGTH '((A B C)));

; MEMBER
(SETQ CLUB '(TOM HARRY JOHN DANIEL))
;위에 setq print 안나옴
(MEMBER 'HARRY CLUB)

; ASSOC
(ASSOC 'TWO '((ONE 1)(TWO 2)(THREE 3)))

; REMOVE
(SETQ MYLIST '(A B C D E F))
(REMOVE 'D MYLIST)

(SETQ MYLIST '(A D B C D E D F))
(REMOVE D MYLIST)

; SUBST
(SUBST 'GOOD 'BAD '(I AM BAD))

; 3. LISP의 Predicate 함수
(ATOM X)

(NULL NIL)
(NULL 0)

(NUMBERP 1)
(NUMBERP "asdf")

(ZEROP 0)
(ZEROP 1)

(MINUSP -1)
(MINUSP 1)

(EQUAL 1 1)
(EQUAL 1 2)

(< 1 2)
(< 2 1)

(>= 2 1)
(>= 1 2)

(STRINGP "A")
(STRINGP #\A)
(STRINGP '(A B C))
(STRINGP 1.2)
(STRINGP 'A)
(STRINGP #(0 1 2))
(STRINGP NIL)

;LISP의 조건문
; IF
(SETQ X 4)
(IF (> X 3) (PRINT X));
(SETQ X 2)
(IF (> X 3) (PRINT X) (+ X 5))

;COND
(COND ((> X 0) (+ X 1))
((= X 0) (+ X 2))
((< X 0) (+ X 3)))