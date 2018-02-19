; Using a=100nm convention

(define-param r 1.25)
(define-param l 16)
(define-param s (* l r))
(define-param w 4)
(define-param d (/ l 16))
(define-param dpml (/ s 16))
(define-param sx s)
(define-param sy s)
(define-param fcen 0.2)
(define-param df 0.3)
(define-param res 16)

(set-param! resolution res)
(set! eps-averaging? false)
(set! k-point (vector3 0 0 0))
(set! ensure-periodicity true)

(set! geometry-lattice (make lattice (size sx sy no-size)))
(define geom (list
  (make block
    (center 0 (/ (+ w d) 2))
    (size l d infinity)
    (material metal)
  )
  (make block
    (center 0 (/ (+ w d) -2))
    (size l d infinity)
    (material metal)
  )
  (make block
    (center 0 (/ (+ l d) 2))
    (size d w infinity)
    (material metal)
  )
  (make block
    (center 0 (/ (+ l d) -2))
    (size d w infinity)
    (material metal)
  )
))

(set! geometry geom)

(set! pml-layers (list (make pml
  (thickness dpml)
)))

(set! sources (list (make source
  (src (make gaussian-src
    (frequency fcen)
    (fwidth df)
  ))
  (component Ez)
  (center 0)
  (size 0 0)
)))

(use-output-directory)

(run-sources+ 100
  (at-beginning output-epsilon)
  (after-sources
    (harminv Ez
      (vector3 0 0)
      fcen
      df
    )
  )
)

(run-until (/ 1 fcen)
  (to-appended "ez" (at-every (/ 1 fcen 20) output-efield-z))
)
