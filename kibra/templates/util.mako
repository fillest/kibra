<%def name="compact(sep='')" filter="trim">
    ## trim whitespace around each line, drop empty and join with sep
    ## usage: <%common:compact [sep='...']>...markup...</%common:compact>
    ## returns: compacted unescaped content
    ## TODO? also replace \s+ with ' '
    ${sep.join(
        filter(None, (line.strip() for line in capture(caller.body).splitlines()))
      ) |n}
</%def>
