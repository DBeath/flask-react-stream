
var Entry = React.createClass({
  render: function() {
    return (
      <div className="entry">
        <span>{this.props.posted}</span>
        <span>{this.props.text}</span>
      </div>
    );
  }
});

var EntryList = React.createClass({
  getInitialState: function() {
    return {data: []};
  },
  componentDidMount: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({data: data.entries});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  render: function() {
    var entryNodes = this.state.data.map(function (entry) {
      return (
        <Entry
          posted = {entry.posted}
          text = {entry.text}
          key = {entry.id}>
        </Entry>
      );
    });
    return (
      <div className="entryList">
        {entryNodes}
      </div>
    );
  }
});

var EntryBox = React.createClass({
  render: function() {
    console.log(this.props)
    return (
      <div className="entryBox">
        <h3>Entries</h3>
        <EntryList data={this.props.entries} />
      </div>
    );
  }
});


ReactDOM.render(
  <EntryList url="/entries" />,
  document.getElementById('content')
);
