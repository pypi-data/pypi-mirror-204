Helps to prevent import of certain modules from certain modules.

It's useful if you have many modules in your project and want to keep them kind of
isolated.

After installing just add `import-rules` option to your `setup.cfg` file.

```
[flake8]
...
import-rules= 
	# yaml format here
	- module_one: [
		module_two allow,
		any deny
	]
	- module_two: [
		module_one.sub.submodule deny
	]
	- module_two.sumbodule: module_one deny
	- module_three: any allow

	# many section for the same module are allowed
	# for example
	- module_two: [
		deny some_other_module
	]

	# this will prevent any import everywhere
	- any: [
		any deny
	]

	# default behaviour is
	- any: [
		any allow
	]

	# For each module (among foo bar baz) allow import from self submodules 
	# and top module of others but not from submodules
	- X | Y | foo | bar | baz : [
		Y.ANY deny,
		Y     allow,
		X 	  allow

	]

...
```
Rules are checking top-down. The Order Matters.

If current module name match section name or is submodule, then it will check all imports by rules from the section.

There can be one or more rules in section.
There can be one or more sections for the same module/submodule.

`modulepath allow` - means allow imports from `modulepath` and its submodules

`modulepath deny` - means deny imports from `modulepath` and its submodules.

Keyword `any` or `ANY` or `all` or `ALL` - menas any module (like `*`)

To combine different module paths in one rule we can use `|` symbol. For example
to define rule for foo.hi foo.low bar.hi bar.low we can use 
`foo|bar.hi|low` . 

We can "define" variable that will be valid only during one section and its rules.
```
A | B | foo | bar | baz : [
	...
]
```
means if current module name is foo or bar or baz then A is equal to current module name
and B will correspond other names from group foo|bar|baz without current module name.

Variable name can be only single uppercase character. You can use variable name in section rule and inside section.

You can use variables for different module level for example

```
X|mod_a|mod_b.domain.Y : [
	X.infra.Y allow
	X.infra.ANY deny
]
```

   
CAUTION. As .INI configparser ignores indentation use `[ ... , .. ]` flow for lists as in example.

