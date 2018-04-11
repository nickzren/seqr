import React from 'react'
import PropTypes from 'prop-types'

import { Table } from 'semantic-ui-react'
import { connect } from 'react-redux'

import TableLoading from 'shared/components/table/TableLoading'

import { getProjectDetailsIsLoading } from '../../reducers'
import TableHeaderRow from './header/TableHeaderRow'
import TableFooterRow from './TableFooterRow'
import EmptyTableRow from './EmptyTableRow'
import FamilyRow from './FamilyRow'
import IndividualRow from './IndividualRow'
import { getVisibleSortedFamiliesWithIndividuals } from '../../utils/visibleFamiliesSelector'

const FamilyTable = ({ visibleFamilies, loading, showHeaderStatusBar, showInternalFields, editCaseReview }) =>
  <Table celled style={{ width: '100%' }}>
    <Table.Body>
      <TableHeaderRow showStatusBar={showHeaderStatusBar} />
      {loading ? <TableLoading /> : null}
      {
        !loading && visibleFamilies.length > 0 ?
          visibleFamilies.map((family, i) =>
            <Table.Row key={family.familyGuid} style={{ backgroundColor: (i % 2 === 0) ? 'white' : '#F3F3F3' }}>
              <Table.Cell style={{ padding: '5px 0px 15px 15px' }}>
                {[
                  <FamilyRow key={family.familyGuid} family={family} showInternalFields={showInternalFields} />,
                  family.individuals.map(individual => (
                    <IndividualRow
                      key={individual.individualGuid}
                      family={family}
                      individual={individual}
                      editCaseReview={editCaseReview}
                    />),
                  ),
                ]}
              </Table.Cell>
            </Table.Row>)
          : <EmptyTableRow />
      }
      <TableFooterRow />
    </Table.Body>
  </Table>

export { FamilyTable as FamilyTableComponent }

FamilyTable.propTypes = {
  visibleFamilies: PropTypes.array.isRequired,
  loading: PropTypes.bool,
  showHeaderStatusBar: PropTypes.bool,
  showInternalFields: PropTypes.bool,
  editCaseReview: PropTypes.bool,
}

const mapStateToProps = state => ({
  visibleFamilies: getVisibleSortedFamiliesWithIndividuals(state),
  loading: getProjectDetailsIsLoading(state),

})

export default connect(mapStateToProps)(FamilyTable)
