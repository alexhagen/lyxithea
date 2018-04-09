# AH_Paper

`ah_paper` is a fork of [`Paper-Now`](https://peerj.github.io/paper-now/).  While `Paper-Now` is ambitious in how it will change publishing for all academics, `ah_paper` is somewhat more conservative.  The goal of `ah_paper` is to provide a development platform for papers that will allow for the publishing of the paper through traditiational routes, but also provide an easy pathway for Author's Draft publication on the internet.  This manifests itself in the following pipeline:

1. Fork the "ah_paper" repository
2. Rename the "ah_paper" repository to a descriptive name
3. Write paper, or import paper, in LaTeX format (or LyX)
4. Track revisions and reviewer comments through review process
5. Upon publication, use the provided python script to convert the LaTeX formatted paper into the `ah_paper` required markdown files
6. commit these files and push to publish.
7. Now you have a legally published, open source edition of your Author's copy that you can send links to or can be discovered on your personal Github.


## To-Do

- [x] Study and review Author's Draft Copyright rules from major journals
	- [x] Checked Elsevier's library and found that Pre-print or final-manuscript works best for our needs
- [ ] Adjust Paper-Now's template to something a touch snazzier
	- [x] Updated sass and some styles
	- [x] Update Figure
	- ~~Update head banner~~
	- [ ] Update tables
	- [x] Update references
- [ ] Develop the python script for LaTeX conversion
- [ ] Add major journal template support (ASME,...)
- [ ] Develop a LyX module to allow for automatic exporting through the LyX GUI
