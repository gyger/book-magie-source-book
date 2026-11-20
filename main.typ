#import "@preview/mousse-notes:2.0.1": *

#set document(
  title: [A Source Book in Physics],
  author: "William Francis Magie",
)

#set page(paper: "iso-b5")
#set figure(supplement: [Fig.])
#set figure.caption(separator: [.])

// This must be the last show or set rule for mousse-notes indent handling.
#show: style

#include "frontmatter.typ"
#include "ch01.typ"
#include "ch02.typ"
#include "ch03.typ"
#include "ch04.typ"
#include "ch05.typ"
