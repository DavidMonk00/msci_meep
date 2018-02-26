(define-param w 10)
(define-param l 20)
(define-param h 10)
(define-param sx w)
(define-param sy l)
(define-param sz h)
(define-param stripH 1)
(define-param stripW 2)
(define-param dpml 0.1)
(define-param res 7)
(define-param freq 0.1)

(set-param! resolution res)
(set! eps-averaging? false)
(set! k-point (vector3 0 0 0))
(set! ensure-periodicity true)

(set! geometry-lattice (make lattice (size sx sy sz)))
(define geom (list
  ; Substrate dielectric
  (make block
    (center 0 0 (/ h 4))
    (size w l (/ h 2))
    (material (make dielectric (epsilon 12)))
  )
  ; centre strip
  (make block
    (center 0 0 (/ stripH 2))
    (size stripW l stripH)
    (material metal)
  )
  ; ground plates
  (make block
    (center (/ (- w stripW) 2) 0 (/ stripH 2))
    (size stripW l stripH)
    (material metal)
  )
  (make block
    (center (/ (- w stripW) -2) 0 (/ stripH 2))
    (size stripW l stripH)
    (material metal)
  )
))

(set! geometry geom)

(set! pml-layers (list (make pml
  (thickness dpml)
)))

(use-output-directory)

(set! sources (list
  (make source
    (src (make continuous-src
      (frequency freq)
      (width 20)
      (end-time (/ 10 freq))
    ))
    (component Ez)
    (center 0 (- (/ l 5) (/ l 2)) 2)
    (size 0 0)
  )
))

(run-until (/ 40 freq)
  (to-appended "ez" (at-every 1 output-efield-z))
)
