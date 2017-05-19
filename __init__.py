from IPython.display import display, Javascript, HTML

display(Javascript("""
MathJax.Hub.Register.StartupHook("TeX Jax Ready",function () {
  var MML = MathJax.ElementJax.mml,
      TeX = MathJax.InputJax.TeX;

  TeX.Definitions.macros.nicefrac = "myBevelFraction";

  TeX.Parse.Augment({
    myBevelFraction: function (name) {
      var num = this.ParseArg(name),
          den = this.ParseArg(name);
      this.Push(MML.mfrac(num,den).With({bevelled: true}));
    }
  });
  MathJax.Hub.Insert(MathJax.InputJax.TeX.Definitions.macros,{
      cancel: ["Extension","cancel"],
      bcancel: ["Extension","cancel"],
      xcancel: ["Extension","cancel"],
      cancelto: ["Extension","cancel"]
    });
});
"""))

display(HTML(r'$\newcommand{\unit}[1]{\mathrm{#1}}$'))
display(HTML(r'$\newcommand{\ce}[1]{\mathrm{#1}}$'))

display(HTML('<link rel="stylesheet" href="https://cdn.rawgit.com/tiaanduplessis/wenk/master/dist/wenk.css">'))
display(HTML('<style> span.abbr{ color: #999; } </style>'))
display(HTML('<style> [data-wenk]:after { z-index: 1000000000; } </style>'))
