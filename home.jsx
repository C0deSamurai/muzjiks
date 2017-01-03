const ServerURL = "127.0.0.1:5000";

const pageHeaderInstance = (
    <PageHeader>MUZJIKS <small>A Scrabble word search tool</small></PageHeader>
)

class DictionaryForm extends React.Component {
    constructor() {
	super();
	this.state = {lexicon: "OWL2"};

	this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event) {
	this.setState({lexicon: event.target.value})
    }

    createOption(name) {
	return (
	    <option key={name} value={name}>{name}</option>
	)
    }

    createSelectItems() {
	let items = [];
	items.push(this.createOption(this.state.lexicon));
	
	$.getJSON(SERVER_URL + "/list-lexicons", function (data) {
	    $.each(data, function(lexiconChoice) {
		if (lexiconChoice != this.state.lexicon) {
		    items.push(this.createOption(lexiconChoice));
		}
	    });
	});
	return items;
    }

    render() {
	return (
	    <FormControl onChange={this.handleChange} componentClass="select" placeholder="select" />
	      {this.createSelectItems()}
	    </FormControl>
	)
    }
}

class WordList extends React.Component {
    tabluateWords() {
	items = [];
	$.each(this.props.words, function(word) {
	    var hooks = $.getJSON(SERVER_URL + '/' + this.props.lexicon + "/hooks/" +
				  word);
	    var fhooks = hooks[0];
	    var bhooks = hooks[1];
	    items.push(<tr><td>{fhooks.join('')}</td><td>{word}</td><td>{bhooks.join('')}</td></tr>);
	});
	return items;
    }
    
    render() {
	return (
	    <Table responsive hover>
		<thead>
		    <tr>
			<th>Front Hooks</th>
			<th>Word</th>
			<th>Back Hooks</th>
		    </tr>
		</thead>
		{this.tabulateWords()}
	    </Table>
	)
    }
}
