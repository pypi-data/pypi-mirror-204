import React, { useState, useContext } from 'react';
import PropTypes from 'prop-types';
import WidgetContext from '../utils/widgetContext';
import axios from 'axios';
import Modal from 'react-modal';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faChevronRight,
  faHome,
  faTimes,
  faTrash,
  faCheckCircle,
} from '@fortawesome/free-solid-svg-icons';

import './ReferenceField.less';

const Breadcrumbs = ({ fetchData, breadcrumbs }) => (
  <div className="modal-breadcrumbs">
    <a
      className="breadcrumb home"
      href="#"
      onClick={e => {
        e.preventDefault();
        fetchData({ path: null, breadcrumbs: [] });
      }}
      title="Home"
    >
      <FontAwesomeIcon icon={faHome} />
    </a>
    {breadcrumbs.map((breadcrumb, idx) => (
      <React.Fragment key={`breadcrumb-${breadcrumb.UID}`}>
        {' '}
        /{' '}
        {idx + 1 < breadcrumbs.length ? (
          <a
            className="breadcrumb"
            href="#"
            onClick={e => {
              e.preventDefault();
              const newBreadcrumbs = JSON.parse(JSON.stringify(breadcrumbs));
              fetchData({
                path: breadcrumb.path,
                breadcrumbs: newBreadcrumbs.slice(0, idx + 1),
              });
            }}
          >
            {breadcrumb.Title}
          </a>
        ) : (
          <span>{breadcrumb.Title}</span>
        )}
      </React.Fragment>
    ))}
  </div>
);

const ItemElement = ({ isSelected, result, onAddReference }) => {
  const { getTranslationFor } = useContext(WidgetContext);

  if (isSelected) {
    return (
      <span className="content-title">
        {result.Title} <FontAwesomeIcon icon={faCheckCircle} />
      </span>
    );
  }
  return (
    <a
      href="#"
      className="content-title"
      title={getTranslationFor('Add') + ' ' + result.Title}
      onClick={e => {
        e.preventDefault();
        onAddReference(result);
      }}
    >
      {result.Title}
    </a>
  );
};

const ReferenceField = ({ value, id, row, items }) => {
  const { root } = items;
  const { updateField, getTranslationFor } = useContext(WidgetContext);
  const [modalIsOpen, setModalOpenState] = useState(false);
  const [modalData, setModalData] = useState({
    results: [],
    total: 0,
    loaded: 0,
    batchPage: 0,
    path: root,
    breadcrumbs: [],
  });
  const selectedUIDs = value ? value.map(item => item.UID) : [];
  const openModal = e => {
    e.preventDefault();
    setModalOpenState(true);
  };
  const closeModal = () => {
    setModalOpenState(false);
  };

  const onAddReference = item => {
    const newValue = value.map(val => val);
    newValue.push(item);
    updateField({ row, id, value: newValue });
  };

  const customStyles = {
    overlay: {
      zIndex: 1000,
    },
    content: {
      top: '50%',
      left: '50%',
      right: 'auto',
      bottom: 'auto',
      marginRight: '-50%',
      transform: 'translate(-50%, -50%)',
      zIndex: 1001,
      maxHeight: '95vh',
      overflow: 'hidden',
    },
  };

  const fetchData = ({ path = null, page = 1, breadcrumbs = null }) => {
    const portalUrl = document.body.getAttribute('data-base-url');
    const queryPath = path ? `${root}${path}` : `${root}`;
    const batchSize = 10;
    axios
      .get(`${portalUrl}/@@getVocabulary`, {
        params: {
          name: 'plone.app.vocabularies.Catalog',
          attributes:
            'UID,Title,portal_type,path,getURL,getIcon,is_folderish,review_state',
          query: {
            criteria: [
              {
                i: 'path',
                o: 'plone.app.querystring.operation.string.path',
                v: `${queryPath}/::1`,
              },
            ],
            sort_on: 'path',
            sort_order: 'ascending',
          },
          batch: { page, size: batchSize },
        },
        headers: { Accept: 'application/json' },
      })
      .then(data => {
        let newLoaded;
        if (page == 1) {
          // first page
          newLoaded = batchSize;
        } else {
          newLoaded = modalData.loaded + batchSize;
        }
        setModalData({
          ...modalData,
          breadcrumbs: breadcrumbs || modalData.breadcrumbs,
          results:
            page > 1
              ? modalData.results.concat(data.data.results)
              : data.data.results,
          total: data.data.total,
          batchPage: page,
          loaded: newLoaded > data.data.total ? data.data.total : newLoaded,
          path,
        });
      });
  };

  const afterOpenModal = () => {
    fetchData({ path: null });
  };

  return (
    <div className="reference-field-wrapper">
      {value.length > 0 && (
        <div className="references">
          {value.map(ref => (
            <div key={`ref-${ref.UID}`} className="reference">
              <button
                className="destructive"
                type="button"
                onClick={e => {
                  e.preventDefault();
                  const newValue = value.filter(val => val.UID !== ref.UID);
                  updateField({ row, id, value: newValue });
                }}
                title={getTranslationFor('Delete')}
              >
                <FontAwesomeIcon icon={faTrash} />
              </button>
              <a href={ref.getURL} target="_blank" rel="noopener noreferrer">
                {ref.Title}
              </a>
              <span
                className="discreet"
                style={{ marginLeft: '1rem', display: 'inline-block' }}
              >
                {ref.path}
              </span>
            </div>
          ))}
        </div>
      )}
      <button onClick={openModal}>
        {getTranslationFor('Select contents')}
      </button>
      <Modal
        isOpen={modalIsOpen}
        onAfterOpen={afterOpenModal}
        onRequestClose={closeModal}
        style={customStyles}
        ariaHideApp={false}
      >
        <button
          className="close"
          onClick={closeModal}
          title={getTranslationFor('Close')}
        >
          <FontAwesomeIcon icon={faTimes} />
        </button>
        <div className="modal-content-wrapper">
          <h2>{getTranslationFor('Select contents')}</h2>
          <p className="discreet">
            {getTranslationFor(
              'Navigate through site structure and select one or more contents.',
            )}
          </p>

          <Breadcrumbs
            fetchData={fetchData}
            breadcrumbs={modalData.breadcrumbs}
          />
          <div className="content-results-wrapper">
            {modalData.results.map(result => {
              const isSelected = selectedUIDs.includes(result.UID);
              return (
                <div
                  className={`content-item ${
                    isSelected ? 'selected-item' : ''
                  }`}
                  key={result.UID}
                >
                  <ItemElement
                    isSelected={isSelected}
                    result={result}
                    onAddReference={onAddReference}
                  />
                  {result.is_folderish && (
                    <button
                      type="button"
                      onClick={() => {
                        let { breadcrumbs } = modalData;
                        breadcrumbs.push({
                          Title: result.Title,
                          UID: result.UID,
                          path: result.path,
                        });
                        fetchData({ path: result.path, breadcrumbs });
                      }}
                      title={getTranslationFor('Expand')}
                    >
                      <FontAwesomeIcon icon={faChevronRight} />
                    </button>
                  )}
                </div>
              );
            })}
          </div>

          {modalData.loaded < modalData.total && (
            <button
              className="context"
              type="button"
              onClick={() => {
                fetchData({
                  path: modalData.path,
                  page: modalData.batchPage + 1,
                });
              }}
            >
              {getTranslationFor('Load more')}
            </button>
          )}
        </div>
      </Modal>
    </div>
  );
};

Breadcrumbs.propTypes = {
  breadcrumbs: PropTypes.array,
  fetchData: PropTypes.func,
};

ReferenceField.propTypes = {
  items: PropTypes.object,
  value: PropTypes.array,
  id: PropTypes.string,
  row: PropTypes.number,
};

ItemElement.propTypes = {
  isSelected: PropTypes.bool,
  result: PropTypes.object,
  onAddReference: PropTypes.func,
};

export default ReferenceField;
